/* eslint-disable react/prop-types */
import { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import Spinner from "./spinner";

const FileUpload = ({ urls }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("page_links", JSON.stringify(urls));

      try {
        setUploading(true);
        const response = await axios.post(
          "https://www.uxlive.me/api/submit-csv/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        setUploading(false);
        console.log(response.data);
        toast.success(JSON.stringify(response?.data?.success));

        // Optionally, you can display a success message to the user.
      } catch (error) {
        setUploading(false);
        console.error("Error uploading file:", error);
        // Handle the error and display an error message to the user.
        toast.error(error ? error?.response?.data?.error : error?.message);
        console.error("Form data submission failed:", error);
      }
    } else {
      console.log("No file selected.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="container mx-auto bg-white max-w-[800px]">
        <label className="block mb-2 mt-4 font-bold" htmlFor="file_input">
          Upload file
        </label>

        <input
          // className="border block w-full p-2.5 rounded-md focus:outline-none focus:outline-[#005734]"
          className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-[#005734] w-full p-2.5"
          id="file_input"
          type="file"
          onChange={handleFileChange}
        />

        <div className="flex flex-row gap-2 justify-center">
          <button
            disabled={!selectedFile || uploading}
            className="mt-3 bg-green-700 hover:bg-green-600 text-white font-bold py-2 pb-0 px-4 rounded flex items-center"
          >
            {/* {uploading ? "Uploading and Submitting..." : "Upload"} */}
            <p>{uploading ? <Spinner /> : "Upload and Submit"}</p>
          </button>
        </div>
      </div>
    </form>
  );
};

export default FileUpload;
