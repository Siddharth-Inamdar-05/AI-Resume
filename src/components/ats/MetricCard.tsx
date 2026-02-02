import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  suffix?: string;
  trend?: 'up' | 'down' | 'neutral';
}

const MetricCard = ({ icon: Icon, label, value, suffix }: MetricCardProps) => {
  return (
    <div className="metric-card">
      <div className="flex items-start justify-between">
        <div className="p-2 rounded-lg bg-primary/10">
          <Icon className="w-4 h-4 text-primary" />
        </div>
      </div>
      <div className="mt-4">
        <p className="text-2xl font-bold text-foreground">
          {value}
          {suffix && <span className="text-base font-normal text-muted-foreground ml-1">{suffix}</span>}
        </p>
        <p className="text-sm text-muted-foreground mt-1">{label}</p>
      </div>
    </div>
  );
};

export default MetricCard;
