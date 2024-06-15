"use client";

import { useState } from "react";
import { ChooseFileStep } from "@/components/ChooseFileStep";
import { ConvertFileStep } from "@/components/ConvertFileStep";
import { DownloadFileStep } from "@/components/DownloadFileStep";

type Step = "CHOOSE_FILE" | "CONVERT" | "DOWNLOAD";

export const PowerPointToPdfConverter = () => {
    const [currentStep, setCurrentStep] = useState<Step>("CHOOSE_FILE");
    const [file, setFile] = useState<File | null>(null);
    const [fileUrl, setFileUrl] = useState<string>("");

    const handleFileSelection = (selectedFile: File) => {
        setFile(selectedFile);
        setCurrentStep("CONVERT");
    };

    const handleConversionComplete = (url: string) => {
        setFileUrl(url);
        console.log(url);
        setCurrentStep("DOWNLOAD");
    };

    const handleConvertAgain = () => {
        setFile(null);
        setFileUrl("");
        setCurrentStep("CHOOSE_FILE");
    };

    switch (currentStep) {
        case "CHOOSE_FILE":
            return <ChooseFileStep onFileSelect={handleFileSelection} />;
        case "CONVERT":
            return (
                <ConvertFileStep
                    file={file}
                    onConversionComplete={handleConversionComplete}
                    onConversionCancel={handleConvertAgain}
                />
            );
        case "DOWNLOAD":
            return (
                <DownloadFileStep
                    fileUrl={fileUrl}
                    onConvertAgain={handleConvertAgain}
                />
            );
    }
};
