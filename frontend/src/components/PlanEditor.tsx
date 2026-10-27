import { useStore } from '../store'
// Read-only summary of the dataset-backed schedule selected for new runs.
export default function PlanEditor() {
  const { failId, failScen } = useStore()
  const selected = failScen.find((item: any) => item.failure_scenario_id === failId)
  return (
    <p className="mut" style={{ margin: 0 }}>
      {selected
        ? `${selected.title} is installed before the first tick and follows its dataset event times.`
        : 'No failure schedule is selected.'}
    </p>)
}
