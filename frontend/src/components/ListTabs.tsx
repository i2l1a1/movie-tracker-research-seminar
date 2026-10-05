import type { ListTab } from '../types/listTab'

type Props = {
    value: ListTab
    onChange: (value: ListTab) => void
}

const tabs: { id: ListTab; label: string }[] = [
    { id: 'all', label: 'All' },
    { id: 'upcoming', label: 'Coming soon' },
]

export function ListTabs({ value, onChange }: Props) {
    return (
        <div className="flex gap-1 border-b border-line" role="tablist" aria-label="List views">
            {tabs.map((tab) => {
                const active = value === tab.id
                return (
                    <button
                        key={tab.id}
                        type="button"
                        role="tab"
                        aria-selected={active}
                        onClick={() => onChange(tab.id)}
                        className={`-mb-px border-b-2 px-3 py-2 text-sm transition ${
                            active
                                ? 'border-gold text-cream'
                                : 'border-transparent text-muted hover:text-cream'
                        }`}
                    >
                        {tab.label}
                    </button>
                )
            })}
        </div>
    )
}
