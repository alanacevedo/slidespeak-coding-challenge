import { FC, useState } from "react";
import { LoadingIndicatorIcon } from "@/icons/LoadingIndicatorIcon";
import { cn } from "@/utils/cn";

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

    if (!file) return null;

    const convertFile = async () => {
        setIsConverting(true);

        try {
            const apiEndpoint = `${process.env.NEXT_PUBLIC_API_HOST}/convert`;
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(apiEndpoint, {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            const url: string = data["converted_file_url"];
            onConversionComplete(url);
        } catch (error) {
            console.error("Conversion error:", error);
        } finally {
            setIsConverting(false);
        }
    };

    const formatBytes = (bytes: number, decimals = 2) => {
        if (bytes === 0) return "0 Bytes";
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ["Bytes", "KB", "MB", "GB"];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return (
            parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i]
        );
    };

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

type CompressionSelectBoxProps = {
    checked?: boolean;
    value: string;
    description: string;
};

const SelectBox: FC<CompressionSelectBoxProps> = ({
    checked = true,
    value,
    description,
}) => (
    <label className="group flex cursor-pointer gap-2 rounded-xl border-2 border-blue-200 bg-blue-25 p-4">
        <input
            type="radio"
            name="compression"
            className="hidden"
            defaultChecked={checked}
        />
        <div>
            <div className="grid size-4 place-items-center rounded-full border border-blue-600">
                <div
                    className={cn(
                        "h-2 w-2 rounded-full bg-blue-600 transition-opacity",
                        {
                            "opacity-0 group-hover:opacity-80": !checked,
                        }
                    )}
                />
            </div>
        </div>
        <div className="flex flex-col gap-0.5">
            <span className="text-sm leading-4 text-blue-800">{value}</span>
            <span className="text-sm text-blue-700">{description}</span>
        </div>
    </label>
);

const Loader = () => (
    <div className="flex w-full items-center gap-2 rounded-xl border border-gray-300 p-4">
        <div className="size-7 animate-spin-pretty rounded-full border-4 border-solid border-t-blue-500" />
        <p className="text-sm text-gray-700">Compressing your file...</p>
    </div>
);
