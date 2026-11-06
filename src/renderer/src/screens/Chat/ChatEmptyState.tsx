import { memo } from "react";
import { Timer, Brain, History, BookmarkPlus } from "lucide-react";
import titleLine from "../../assets/title-line.svg";
import { useI18n } from "../../components/useI18n";
import ProfileAvatar from "../../components/common/ProfileAvatar";
import type { AgentAvatarInfo } from "./MessageRow";

interface Suggestion {
  i18nKey: string;
  text: string;
  Icon: typeof Timer;
}

const SUGGESTIONS: Suggestion[] = [
  {
    i18nKey: "chat.suggestionDailyBrief",
    text: "Every weekday at 9 AM, search the web for news on the topics I care about and send me a five-line brief. Ask me which topics first.",
    Icon: Timer,
  },
  {
    i18nKey: "chat.suggestionRemember",
    text: "Ask me five questions about how I like to work, then save my answers to memory.",
    Icon: Brain,
  },
  {
    i18nKey: "chat.suggestionResume",
    text: "Search my past sessions and tell me what I was working on last and what is still unfinished.",
    Icon: History,
  },
  {
    i18nKey: "chat.suggestionSkill",
    text: "Walk me through a task I repeat often, then save it as a skill you can reuse.",
    Icon: BookmarkPlus,
  },
];

interface ChatEmptyStateProps {
  agent?: AgentAvatarInfo;
  onSelectSuggestion: (text: string) => void;
}

export const ChatEmptyState = memo(function ChatEmptyState({
  onSelectSuggestion,
  agent,
}: ChatEmptyStateProps): React.JSX.Element {
  const { t } = useI18n();
  const useProfileAvatar =
    !!agent?.avatar || (!!agent?.name && agent.name !== "default");

  return (
    <div className="chat-empty">
      <div className="chat-empty-icon">
        {useProfileAvatar ? (
          <ProfileAvatar
            name={agent?.name || "default"}
            color={agent?.color}
            avatar={agent?.avatar}
            size={64}
          />
        ) : (
          <span
            className="chat-empty-logo"
            role="img"
            aria-label="Hermes"
            style={{
              maskImage: `url(${titleLine})`,
              WebkitMaskImage: `url(${titleLine})`,
            }}
          />
        )}
      </div>
      <div className="chat-empty-suggestions">
        {SUGGESTIONS.map(({ i18nKey, text, Icon }) => (
          <button
            key={i18nKey}
            className="chat-suggestion"
            onClick={() => onSelectSuggestion(text)}
          >
            <Icon size={16} />
            {t(i18nKey)}
          </button>
        ))}
      </div>
    </div>
  );
});
