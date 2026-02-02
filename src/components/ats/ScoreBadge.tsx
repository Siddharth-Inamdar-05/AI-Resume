interface ScoreBadgeProps {
  score: number;
  showPercentage?: boolean;
}

const ScoreBadge = ({ score, showPercentage = true }: ScoreBadgeProps) => {
  const getBadgeClass = () => {
    if (score >= 80) return 'score-badge score-badge-high';
    if (score >= 50) return 'score-badge score-badge-medium';
    return 'score-badge score-badge-low';
  };

  return (
    <span className={getBadgeClass()}>
      {score.toFixed(1)}{showPercentage && '%'}
    </span>
  );
};

export default ScoreBadge;
