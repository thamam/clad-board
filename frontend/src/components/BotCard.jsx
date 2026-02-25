import { Link } from "react-router-dom";
import StatusBadge from "./StatusBadge";

function timeAgo(dateStr) {
  if (!dateStr) return "Never";
  const seconds = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export default function BotCard({ bot }) {
  return (
    <Link
      to={`/bots/${bot.id}`}
      className="block rounded-lg border border-gray-700 bg-gray-800 p-5 transition hover:border-gray-500"
    >
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">{bot.name}</h3>
        <StatusBadge status={bot.computed_status} />
      </div>

      <p className="mb-3 text-sm text-gray-400">
        Class: <span className="text-gray-300">{bot.bot_class}</span>
      </p>

      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <div>
          <div className="text-gray-400">Heartbeat</div>
          <div className="text-white">{timeAgo(bot.last_heartbeat)}</div>
        </div>
        <div>
          <div className="text-gray-400">Messages</div>
          <div className="text-white">{bot.message_count}</div>
        </div>
        <div>
          <div className="text-gray-400">Errors</div>
          <div className={bot.error_count > 0 ? "text-red-400" : "text-white"}>
            {bot.error_count}
          </div>
        </div>
      </div>
    </Link>
  );
}
