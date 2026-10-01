export type Metric = { samples: number; mae_ug_m3: number; rmse_ug_m3: number; mean_error_ug_m3: number };
export type Evidence = { metadata: { model_id: string; artifact_sha256: string; feature_names: string[]; artifact_bytes: number }; test: { models: Record<string, Metric>; by_recording: Record<string, Record<string, Metric>>; samples: number; mae_improvement_over_persistence_percent: number; descriptive_warnings_by_recording: Record<string, {models: Record<string, {matched_events: number; scored_warnings: number; scorable_events: number}>}> }; training: { sum_fit_seconds: number; candidates: { model_id: string; validation: Metric }[] }; fixture: { history_pm10_ug_m3: number[][]; expected_predictions_ug_m3: number[] } };
export type Site = { team: {name: string; members: string[]; team_id: string | null; team_id_status: string; theme: string}; build_parent_commit: string; problem_source: {title: string; url: string}; costs: null | {checked_date: string; basis: string; currencies: Record<string, number>; items: {name: string; quantity: number; unit_price: number | null; currency: string; source_url: string; note: string}[]; exclusions: string[]} };
export type Episode = {episode_id: string; partition: string; group: number; label: string; file: string; first_issue_second: number; last_issue_second: number; suggested_start_second: number; last_second: number};
export type ReplayIndex = {model_id: string; artifact_sha256: string; task_id: string; attribution: string; source_url: string; episodes: Episode[]};
export type Recording = {episode_id: string; partition: string; pm10_ug_m3: number[]; observation_seconds: number[]; forecast_issue_seconds: number[]; saved_forecast_pm10_ug_m3: number[]; saved_trailing_mean_pm10_ug_m3: number[]};
export type Point = {time_seconds: number; pm10_ug_m3: number};
export type Forecast = {mode: string; model_id: string; artifact_sha256: string; issue_time_seconds: number; target_time_seconds: number; predicted_pm10_ug_m3: number; current_pm10_ug_m3: number; baselines: {persistence_pm10_ug_m3: number; trailing_mean_pm10_ug_m3: number}; features?: Record<string, number>; snapshot_id?: string; inference_milliseconds?: number; input_quality?: {snapshots: number; maximum_observation_age_seconds: number}; crossing_status?: string; crossing_eta_seconds?: null};
export type Snapshot = {episode_id: string; clock_second: number; forecast: Forecast; past_observations: Point[]; request: {history: (Point & {observation_time_seconds: number})[]; issue_time_seconds: number; [key: string]: unknown}; matured_forecast: null | {issue_time_seconds: number; target_time_seconds: number; predicted_pm10_ug_m3: number; actual_pm10_ug_m3: number}; attribution: string};
export type SimMetric = {water_litres: number; mean_max_boundary_pm10_ug_m3: number; peak_boundary_pm10_ug_m3: number; exceedance_seconds: number; zone_switches: number; zone_duty_seconds: Record<string,number>; integrated_max_boundary_exposure_ug_s_m3: number};
export type Diagnostic = {issue_second: number; forecast_status: string; crossings: {status: string; eta_seconds: number | null}[] | null; trajectory: number[][] | null; source_forecast_pm10_ug_m3: number | null; risk_zones: string[]};
export type SimPoint = {second: number; pm10_ug_m3: number[]; commands: boolean[]; effective_misting?: boolean[]; water_litres: number; data_available: boolean; source_proxy_pm10_ug_m3: number | null; wind_from_degrees: number | null; forecast: Diagnostic | null};
export type Strategy = 'no_control' | 'continuous' | 'reactive' | 'predictive';
export const strategyNames: Record<Strategy,string> = {no_control: 'No control', continuous: 'Continuous', reactive: 'Reactive', predictive: 'Predictive'};
export const strategies = Object.keys(strategyNames) as Strategy[];
export type Scenario = {scenario_id: string; name: string; scope: string; environment_sha256: string; predictor_artifact_sha256: string; parameters: {ambient_pm10_ug_m3:number; boundary_setting_ug_m3:number; flow_litres_minute_per_zone:number; wind_speed_metres_second:number; mist_source_fraction_removed:number; minimum_on_seconds:number; minimum_off_seconds:number; actuator_delay_seconds:number; transport_gain:number; forecast_trajectory_rule:string}; case: {wind_from_degrees:number}; runs: Record<Strategy,{metrics: SimMetric; trace: SimPoint[]}>};
export type ScenarioIndex = {scenarios: {id:string; name:string; file:string; metrics:Record<Strategy,SimMetric>}[]};
export async function getJson<T>(url: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(url, {signal});
  if (!response.ok) throw new Error(`${response.status}: ${url}`);
  return response.json();
}
export async function fallbackJson<T>(primary: string, saved: string, signal?: AbortSignal): Promise<T> {
  try { return await getJson<T>(primary,signal); } catch (error) { if (signal?.aborted) throw error; return getJson<T>(saved,signal); }
}
const recordCache = new Map<string,Recording>();
export async function recordedSnapshot(index: ReplayIndex, episode: Episode, second: number, signal?: AbortSignal): Promise<Snapshot> {
  let record = recordCache.get(episode.episode_id);
  if (!record) { record = await getJson<Recording>(`/demo/replay/${episode.file}`,signal); recordCache.set(episode.episode_id,record); }
  const position = record.forecast_issue_seconds.indexOf(second);
  if (position < 0) throw new Error('This recording time has no eligible forecast.');
  const history = Array.from({length:121},(_,i)=>{const t=second-120+i;return {time_seconds:t,pm10_ug_m3:record!.pm10_ug_m3[t],observation_time_seconds:record!.observation_seconds[t]};});
  const previous = record.forecast_issue_seconds.indexOf(second-30);
  return {episode_id:episode.episode_id,clock_second:second,attribution:index.attribution,
    request:{history,issue_time_seconds:second},
    past_observations:Array.from({length:Math.min(second,240)+1},(_,i)=>{const t=Math.max(0,second-240)+i;return {time_seconds:t,pm10_ug_m3:record!.pm10_ug_m3[t]};}),
    matured_forecast:previous<0?null:{issue_time_seconds:second-30,target_time_seconds:second,predicted_pm10_ug_m3:record.saved_forecast_pm10_ug_m3[previous],actual_pm10_ug_m3:record.pm10_ug_m3[second]},
    forecast:{mode:'saved_inference',model_id:index.model_id,artifact_sha256:index.artifact_sha256,issue_time_seconds:second,target_time_seconds:second+30,predicted_pm10_ug_m3:record.saved_forecast_pm10_ug_m3[position],current_pm10_ug_m3:record.pm10_ug_m3[second],baselines:{persistence_pm10_ug_m3:record.pm10_ug_m3[second],trailing_mean_pm10_ug_m3:record.saved_trailing_mean_pm10_ug_m3[position]}}
  };
}
export async function loadScenario(id:string,index:ScenarioIndex):Promise<Scenario> {
  try {return await getJson<Scenario>(`/v1/scenarios/${id}`);} catch {
    const item=index.scenarios.find(item=>item.id===id); if(!item)throw new Error('Unknown scenario');
    const response=await fetch(`/demo/simulation/${item.file}`); if(!response.ok)throw new Error('Saved scenario unavailable');
    const stream=response.body!.pipeThrough(new DecompressionStream('gzip'));
    return JSON.parse(await new Response(stream).text());
  }
}
export const number=(value:number,digits=1)=>value.toLocaleString('en-US',{minimumFractionDigits:digits,maximumFractionDigits:digits});
export const clock=(seconds:number)=>`${Math.floor(seconds/60).toString().padStart(2,'0')}:${Math.floor(seconds%60).toString().padStart(2,'0')}`;
