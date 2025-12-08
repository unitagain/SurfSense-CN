import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";
import { getBearerToken } from "@/lib/auth-utils";
import { logger } from "@/lib/logger";

interface UseApiKeyReturn {
	apiKey: string | null;
	isLoading: boolean;
	copied: boolean;
	copyToClipboard: () => Promise<void>;
}

export function useApiKey(): UseApiKeyReturn {
	const [apiKey, setApiKey] = useState<string | null>(null);
	const [copied, setCopied] = useState(false);
	const [isLoading, setIsLoading] = useState(true);

	useEffect(() => {
		// Load API key from localStorage
		const loadApiKey = () => {
			try {
				const token = getBearerToken();
				setApiKey(token);
			} catch (error) {
				logger.error("Error loading API key:", error);
				toast.error("Failed to load API key");
			} finally {
				setIsLoading(false);
			}
		};

		// Add a small delay to simulate loading
		const timer = setTimeout(loadApiKey, 500);
		return () => clearTimeout(timer);
	}, []);

	const copyToClipboard = useCallback(async () => {
		if (!apiKey) return;

		try {
			if (navigator.clipboard && window.isSecureContext) {
				// Use Clipboard API if available and in secure context
				await navigator.clipboard.writeText(apiKey);
			} else {
				// Fallback for non-secure contexts or browsers without Clipboard API
				const textArea = document.createElement("textarea");
				textArea.value = apiKey;
				textArea.style.position = "fixed";
				textArea.style.left = "-999999px";
				textArea.style.top = "-999999px";
				document.body.appendChild(textArea);
				textArea.focus();
				textArea.select();
				document.execCommand("copy");
				textArea.remove();
			}
			setCopied(true);
			toast.success("API key copied to clipboard");

			setTimeout(() => {
				setCopied(false);
			}, 2000);
		} catch (err) {
			logger.error("Failed to copy:", err);
			toast.error("Failed to copy API key");
		}
	}, [apiKey]);

	return {
		apiKey,
		isLoading,
		copied,
		copyToClipboard,
	};
}
