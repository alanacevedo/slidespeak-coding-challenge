import { FC, useEffect, useState } from "react";
import { LoadingIndicatorIcon } from "@/icons/LoadingIndicatorIcon";
import { SelectBox } from "./SelectBox";
import { Loader } from "./Loader";
import { formatBytes } from "@/utils/formatBytes";

const pollIntervalSeconds = 3;

type ConvertFileStepProps = {
    file: File | null;
    onConversionComplete: (url: string) => void;
    onConversionCancel: () => void;
};

export const ConvertFileStep: FC<ConvertFileStepProps> = ({
    file,
    onConversionComplete,
    onConversionCancel,
}) => {
    const [isConverting, setIsConverting] = useState(false);
    const [taskId, setTaskId] = useState<string | null>(null);

    if (!file) return null;

    const convertFile = async () => {
        setIsConverting(true);

        try {
            const convertEndpoint = `${process.env.NEXT_PUBLIC_API_HOST}/convert`;
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(convertEndpoint, {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            const taskId: string = data["task_id"];
            setTaskId(taskId);
        } catch (error) {
            console.error("Conversion error:", error);
        }
    };

    useEffect(() => {
        if (!taskId) return;

        const interval = setInterval(async () => {
            try {
                const statusEndpoint = `${process.env.NEXT_PUBLIC_API_HOST}/convert/status/${taskId}`;
                const response = await fetch(statusEndpoint);
                const data = await response.json();

                if (data.status === "pending") return;

                // data is ready, or an error ocurred
                clearInterval(interval);
                setIsConverting(false);

                if (data.status === "success") {
                    onConversionComplete(data.converted_file_url);
                } else {
                    // TODO: better error handling
                    alert("Conversion error");
                }
            } catch (error) {
                console.error("Status check error:", error);
                alert("Conversion error");
                clearInterval(interval);
                setIsConverting(false);
            }
        }, pollIntervalSeconds * 1000);

        // cleanup when unmounted
        return () => clearInterval(interval);
    }, [taskId, onConversionComplete]);

    return (
        <div className="flex flex-col gap-4 rounded-xl bg-white p-6 shadow-md">
            <div className="flex w-full flex-col gap-1 rounded-lg border border-gray-300 p-4 text-center">
                <p className="text-lg font-semibold text-gray-800">
                    {file.name}
                </p>
                <p className="text-sm text-gray-600">
                    {formatBytes(file.size)}
                </p>
            </div>
            {isConverting ? (
                <Loader />
            ) : (
                <SelectBox
                    value="Convert to PDF"
                    description="Best quality, retains images and other assets."
                />
            )}

            <div className="flex w-full gap-3">
                <button
                    type="button"
                    disabled={isConverting}
                    title="Cancel"
                    className="w-full rounded-lg border border-gray-300 bg-transparent px-4 py-2.5 font-semibold text-gray-700 shadow-sm disabled:cursor-not-allowed disabled:opacity-30"
                    onClick={onConversionCancel}
                >
                    Cancel
                </button>
                <button
                    type="button"
                    disabled={isConverting}
                    className="flex w-full items-center justify-center rounded-lg border border-blue-600 bg-blue-600 px-4 py-2.5 font-semibold text-white shadow-sm disabled:cursor-not-allowed disabled:opacity-30"
                    onClick={convertFile}
                >
                    {isConverting ? (
                        <div className="animate-spin">
                            <LoadingIndicatorIcon />
                        </div>
                    ) : (
                        "Convert"
                    )}
                </button>
            </div>
        </div>
    );
};
