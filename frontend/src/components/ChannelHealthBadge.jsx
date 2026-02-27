const STATUS_COLORS = {
  connected: "bg-green-500",
  disconnected: "bg-red-500",
  error: "bg-yellow-500",
};

export function ChannelStatusDot({ status }) {
  return (
    <span
      className={`inline-block h-2.5 w-2.5 rounded-full ${STATUS_COLORS[status] || "bg-gray-500"}`}
      title={status}
    />
  );
}

export default function ChannelHealthBadge({ channelsUp, channelsTotal }) {
  if (channelsTotal === 0) return null;

  const allUp = channelsUp === channelsTotal;
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ${
        allUp
          ? "bg-green-900/50 text-green-300"
          : "bg-red-900/50 text-red-300"
      }`}
    >
      <span
        className={`inline-block h-1.5 w-1.5 rounded-full ${allUp ? "bg-green-400" : "bg-red-400"}`}
      />
      {channelsUp}/{channelsTotal} ch
    </span>
  );
}
