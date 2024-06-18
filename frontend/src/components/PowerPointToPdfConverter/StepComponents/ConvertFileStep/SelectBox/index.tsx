import { FC } from "react";
import { cn } from "@/utils/cn";

type CompressionSelectBoxProps = {
    checked?: boolean;
    value: string;
    description: string;
};

export const SelectBox: FC<CompressionSelectBoxProps> = ({
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
