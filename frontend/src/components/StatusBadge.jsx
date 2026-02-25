const statusConfig = {
  online: { color: "bg-green-500", label: "Online" },
  idle: { color: "bg-yellow-500", label: "Idle" },
  offline: { color: "bg-red-500", label: "Offline" },
};

export default function StatusBadge({ status }) {
  const config = statusConfig[status] || statusConfig.offline;

  return (
    <span className="inline-flex items-center gap-1.5 text-sm">
      <span className={`inline-block h-2.5 w-2.5 rounded-full ${config.color}`} />
      {config.label}
    </span>
  );
}
