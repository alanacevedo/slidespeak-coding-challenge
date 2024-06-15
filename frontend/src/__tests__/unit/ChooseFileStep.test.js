import '@testing-library/jest-dom'
import { render, fireEvent, act } from "@testing-library/react";
import { ChooseFileStep } from "@/components/ChooseFileStep";


function mockData(files) {
    return {
        dataTransfer: {
            files,
            items: files.map((file) => ({
                kind: 'file',
                type: file.type,
                getAsFile: () => file,
            })),
            types: ['Files'],
        },
    };
}


describe("ChooseFileStep", () => {
    it("renders correctly", () => {
        const { getByText } = render(<ChooseFileStep onFileSelect={() => { }} />);
        expect(getByText(/Drag and drop a PowerPoint file to convert to PDF/i)).toBeInTheDocument();
    });

    it("calls onFileSelect with the selected file", async () => {

        const handleFileSelect = jest.fn();
        const { getByTestId } = render(<ChooseFileStep onFileSelect={handleFileSelect} />);

        const file = new File(["dummy content"], "TEST PPT.ppt", { name: "TEST PPT.ppt", path: "TEST PPT.ppt", type: "application/vnd.ms-powerpoint" });
        const dropzoneElement = getByTestId('choose-file-step');

        const data = mockData([file]);

        await act(() => {
            fireEvent.drop(dropzoneElement, data)
        })

        expect(handleFileSelect).toBeCalled()
    });
});