import { useParams, Link } from "react-router-dom";
import { useBotDetail } from "../api";
import { ChannelStatusDot } from "../components/ChannelHealthBadge";
import StatusBadge from "../components/StatusBadge";
import TokenTable from "../components/TokenTable";

function formatDuration(seconds) {
  if (!seconds) return "N/A";
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

function Section({ title, children }) {
  return (
    <div className="rounded-lg border border-gray-700 bg-gray-800 p-5">
      <h2 className="mb-3 text-lg font-semibold text-white">{title}</h2>
      {children}
    </div>
  );
}

export default function BotDetail() {
  const { botId } = useParams();
  const { data: bot, isLoading, error } = useBotDetail(botId);

  if (isLoading) {
    return <div className="py-20 text-center text-gray-400">Loading...</div>;
  }
  if (error) {
    return (
      <div className="py-20 text-center text-red-400">
        Failed to load bot: {error.message}
      </div>
    );
  }
  if (!bot) return null;

  return (
    <div>
      <Link to="/" className="mb-4 inline-block text-sm text-blue-400 hover:text-blue-300">
        &larr; All Bots
      </Link>

      <div className="mb-6 flex items-center gap-4">
        <h1 className="text-2xl font-bold text-white">{bot.name}</h1>
        <StatusBadge status={bot.computed_status} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        {/* Identity */}
        <Section title="Identity">
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-400">Class</dt>
            <dd className="text-white">{bot.bot_class}</dd>
            <dt className="text-gray-400">Version</dt>
            <dd className="text-white">{bot.version || "N/A"}</dd>
            <dt className="text-gray-400">Uptime</dt>
            <dd className="text-white">{formatDuration(bot.uptime_seconds)}</dd>
            <dt className="text-gray-400">Status</dt>
            <dd className="text-white capitalize">{bot.status}</dd>
          </dl>
        </Section>

        {/* Configuration */}
        <Section title="Configuration">
          <div className="space-y-3 text-sm">
            <div>
              <span className="text-gray-400">Models: </span>
              <span className="text-white">
                {bot.models?.length > 0 ? bot.models.join(", ") : "None"}
              </span>
            </div>
            <div>
              <span className="text-gray-400">Channels: </span>
              <span className="text-white">
                {bot.channels?.length > 0 ? bot.channels.join(", ") : "None"}
              </span>
            </div>
            <div>
              <span className="text-gray-400">Skills: </span>
              <span className="text-white">
                {bot.skills?.length > 0 ? bot.skills.join(", ") : "None"}
              </span>
            </div>
            {bot.tools?.length > 0 && (
              <div>
                <span className="text-gray-400">Tools: </span>
                <div className="mt-1 flex flex-wrap gap-2">
                  {bot.tools.map((tool) => (
                    <span
                      key={tool.name}
                      className={`rounded px-2 py-0.5 text-xs ${
                        tool.enabled
                          ? "bg-green-900 text-green-300"
                          : "bg-gray-700 text-gray-400"
                      }`}
                    >
                      {tool.name}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Section>

        {/* Channel Health */}
        {bot.channel_statuses?.length > 0 && (
          <Section title="Channel Health">
            <div className="space-y-2">
              {bot.channel_statuses.map((ch) => (
                <div
                  key={ch.channel_name}
                  className="flex items-center justify-between rounded bg-gray-900 px-3 py-2 text-sm"
                >
                  <div className="flex items-center gap-2">
                    <ChannelStatusDot status={ch.status} />
                    <span className="font-medium text-white">{ch.channel_name}</span>
                    <span className="capitalize text-gray-400">{ch.status}</span>
                  </div>
                  <div className="text-right text-xs text-gray-500">
                    {ch.error_message && (
                      <span className="mr-3 text-red-400">{ch.error_message}</span>
                    )}
                    {ch.last_seen
                      ? `Seen ${new Date(ch.last_seen).toLocaleString()}`
                      : ""}
                  </div>
                </div>
              ))}
            </div>
          </Section>
        )}

        {/* Activity */}
        <Section title="Activity">
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-400">Messages In</dt>
            <dd className="text-white">{bot.messages_in}</dd>
            <dt className="text-gray-400">Messages Out</dt>
            <dd className="text-white">{bot.messages_out}</dd>
            <dt className="text-gray-400">Last Message</dt>
            <dd className="text-white">
              {bot.last_message_at
                ? new Date(bot.last_message_at).toLocaleString()
                : "None"}
            </dd>
          </dl>
        </Section>

        {/* Errors */}
        <Section title="Errors">
          <dl className="grid grid-cols-2 gap-2 text-sm">
            <dt className="text-gray-400">Total Errors</dt>
            <dd className={bot.error_count > 0 ? "text-red-400" : "text-white"}>
              {bot.error_count}
            </dd>
            <dt className="text-gray-400">Last Error</dt>
            <dd className="text-white">
              {bot.last_error_message || "None"}
            </dd>
            <dt className="text-gray-400">Last Error At</dt>
            <dd className="text-white">
              {bot.last_error_at
                ? new Date(bot.last_error_at).toLocaleString()
                : "N/A"}
            </dd>
          </dl>
        </Section>
      </div>

      {/* Token Usage — full width */}
      <div className="mt-4">
        <Section title="Token Usage">
          <TokenTable tokenUsage={bot.token_usage} />
        </Section>
      </div>
    </div>
  );
}
