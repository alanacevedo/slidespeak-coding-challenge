import '@testing-library/jest-dom'
import { render, screen } from "@testing-library/react";
import { PowerPointToPdfConverter } from "@/components/PowerPointToPdfConverter";

describe("PowerPointToPdfConverter", () => {
    it("renders the ChooseFileStep initially", () => {
        render(<PowerPointToPdfConverter />);
        const chooseFileStep = screen.getByTestId("choose-file-step");
        expect(chooseFileStep).toBeInTheDocument();
    });
});