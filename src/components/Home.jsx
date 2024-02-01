import axios from "axios";
import { useState } from "react";
import DynamicForm from "./DynamicForm";
import { toast } from "react-toastify";
import { FaFileExcel } from "react-icons/fa";
import { v4 as uuidv4 } from "uuid";
import FileUpload from "./Upload";
import Accordion from "./accordion";
import Spinner from "./spinner";
import OccurenceModal from "./Modal";

const Home = () => {
  const [formData, setFormData] = useState();
  const [loadingCreate, setLoadingCreate] = useState(false);
  const [loadingDownload, setLoadingDownload] = useState(false);
  const [link, setLink] = useState({});
  const [linksUrl, setLinksUrl] = useState([]);
  const [loading, setLoading] = useState(false);
  const [occurrence, setOccurrence] = useState(null);
  const [showOccurrence, setShowOccurrence] = useState(false);

  const [loadingGetOccurence, setLoadingOccurence] = useState(false);

  const [modalOpen, setModalOpen] = useState(false);

  const links = linksUrl?.map(({ item }) => item);
  const [email, setEmail] = useState("");

  const handleOccurrence = async () => {
    let response = null;
    setLoadingOccurence(true);
    // Prepare the data to send to the backend
    try {
      response = await axios.get(
        `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=get_user_email&product_number=UXLIVINGLAB007&email=${email}`
      );
      if (response.data.occurrences === 0) {
        await axios.post(
          `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=register_user`,
          {
            product_number: "UXLIVINGLAB007",
            email: email,
          }
        );
      }
      setLoadingOccurence(false);
      setOccurrence(response.data.occurrences);
      setShowOccurrence(true);
      setModalOpen(true);
      console.log("ShowModal", modalOpen);
    } catch (e) {
      setLoadingOccurence(false);
      console.log("Error", e);
    }
  };

  const handleFormData = async () => {
    try {
      setLoadingCreate(true);
      const response = await axios.post(
        `https://www.uxlive.me/api/contact-us-extractor/`,
        {
          page_links: links,
        }
      );
      response?.data && handleSendEmail(response.data);
      setFormData(response?.data);
      setLoading(false);
      setShowOccurrence(false);
      setLoadingCreate(false);
      console.log("formData", formData);
    } catch (error) {
      setLoadingCreate(false);
      console.log(error);
      if (error?.response?.data?.page_links) {
        toast.error("Enter a valid URL");
      } else {
        toast.error(error?.message);
      }
    }
  };

  const handleScrapeForm = async (ev) => {
    ev.preventDefault();
    //delete id from the objects array and take the link
    handleOccurrence();
  };
  const handleInputLinks = (event) => {
    if (
      event.target.value[event.target.value.length - 1] === " " &&
      link.item.trim() !== ""
    ) {
      setLinksUrl([...linksUrl, link]);
      setLink({});
      event.target.value = "";
    } else {
      setLink({ id: `${uuidv4()}`, item: event.target.value });
    }
  };
  const handleEnterKey = (event) => {
    if (event.key === "Enter" && link.item.trim() !== "") {
      setLinksUrl([...linksUrl, link]);
      setLink({});
      event.target.value = "";
    }
  };

  const handleDeleteLink = (itemId) => {
    setLinksUrl(linksUrl.filter(({ id }) => id !== itemId));
  };

  const handleDownLoadFile = async () => {
    try {
      setLoadingDownload(true);

      const response = await axios.post(
        `https://www.uxlive.me/api/download-csv/?file_type=xlsx`,
        {
          page_links: links,
        },
        { responseType: "blob" }
      );

      // Extract the filename from the Content-Disposition header
      const contentDisposition = response.headers["content-disposition"];
      let filename = ""; // Default filename
      if (contentDisposition) {
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        let matches = filenameRegex.exec(contentDisposition);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, "");
        }
      }

      const blob = new Blob([response.data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename; // Use the extracted filename
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      toast.success("File downloaded successfully");
      setLoadingDownload(false);
    } catch (error) {
      setLoadingDownload(false);
      console.log(error);
      if (error?.response?.data?.error) {
        toast.error(error?.response?.data?.error);
      } else {
        toast.error(error?.message);
      }
    }
  };

  // function to send extracted data to email
  const handleSendEmail = async (datas) => {
    try {
      // setLoading(true);

      const htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DoWell "Contact Us Page" Extractor</title>
      </head>
      <body>
        <div style="font-family: Helvetica, Arial, sans-serif; min-width: 100px; overflow: auto; line-height: 2">
          <div style="margin: 50px auto; width: 70%; padding: 20px 0">
            <div style="border-bottom: 1px solid #eee">
              <a href="#" style="font-size: 1.2em; color: #00466a; text-decoration: none; font-weight: 600">Dowell UX Living Lab</a>
            </div>
            <p style="font-size: 1.1em">Email : ${email}</p>
            
            <p style="font-size: 1.1em">Extracted Form Fields</p> ${" "}
            <ul>
              ${Object.entries(datas)
                .map(
                  ([name, value]) => `<li key=${name}>${name} : ${value}</li>`
                )
                .join("")}
            </ul>
          </div>
        </div>
      </body>
    </html>
  `;

      const response = await axios.post(
        `https://100085.pythonanywhere.com/api/email/`,
        {
          toname: "Dowell UX Living Lab",
          toemail: !email ? "dowell@dowellresearch.uk" : email,
          subject: `${email} result from DoWell "Contact Us Page" Extractor on ${new Date()}`,
          email_content: htmlContent,
        }
      );
      // Set the emailSent state to true when the email is sent

      console.log(response);
    } catch (error) {
      toast.error(error ? error?.response?.data?.error : error?.message);
      console.log(error);
    }
  };

  return (
    <div className="page-container">
      <div style={{ width: "100%", height: "100%" }}>
        <div>
          <div className="container">
            {showOccurrence && modalOpen && (
              <OccurenceModal
                email={email}
                showModal={modalOpen}
                setOpenModal={setModalOpen}
                showOccurrence={showOccurrence}
                occurrence={occurrence}
                handleFormData={handleFormData}
              />
            )}

            <div className="mx-auto overflow-hidden max-w-[800px]">
              {/* Logo */}
              <div className="flex justify-center my-4">
                <img
                  src="https://www.uxlivinglab.org/wp-content/uploads/2023/10/image_1-3.png"
                  className="flex justify-center"
                  alt="Dowell Logo"
                />
              </div>

              <hr className="col-md-10 pb-3" />

              {/* Email Extractor Title */}
              <h1 className="text-center font-bold text-[#005734]">
                {" "}
                DoWell &quot;Contact Us Page&quot; Extractor{" "}
              </h1>

              {/*  About Email Extractor */}
              <p className="subTitle mt-5 mb-3">
                Introducing the ultimate &quot;contact us&quot; form extraction
                and submission tool. Extract &quot;contact us&quot; form from
                any webpage instantly. Fill it out directly or download as
                spreadsheet for offline editing.
                <br />
                <br />
                Effortlessly submit forms at their original location. Simplify
                your form interaction today!
              </p>

              {/* Link Form and 2 Buttons */}
              <div className="flex flex-col mt-4">
                <div
                  tabIndex={0}
                  className="flex-grow bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:border-[#005734] w-full p-2.5"
                >
                  {linksUrl.map(({ item, id }) => (
                    <button
                      key={id}
                      className="border border-0.15 rounded-md p-1 hover:bg-green-700 text-white bg-[#005734] mr-1"
                    >
                      {item}
                      <small
                        onClick={() => handleDeleteLink(id)}
                        className="text-red-500 text-md m-2 mr-0.5 rounded-full bg-green-200 p-0.5 px-2 font-semibold"
                      >
                        X
                      </small>
                    </button>
                  ))}
                  <input
                    id="my-input"
                    onChange={handleInputLinks}
                    onKeyDown={handleEnterKey}
                    placeholder="Enter the Website Url or Link Here"
                    className="border-none bg-gray-50 focus:border-none focus:outline-none w-64"
                  />
                </div>

                <div className="mb-4 text-xs text-gray-500">
                  Press enter or space after each entry.
                </div>

                <input
                  type="email"
                  // border-2 border-green-500 focus:outline-none focus:border-green-500 p-2
                  className="border border-gray-300 flex mb-3 bg-gray-50 focus:outline-none text-gray-900 rounded-lg focus:border-[#005734] w-full p-2.5"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="dowell@dowellresearch.uk "
                />

                <div className="flex flex-row gap-2 justify-center">
                  <button
                    onClick={handleScrapeForm}
                    disabled={links.length < 1 || loadingCreate}
                    className="bg-green-700 hover:bg-green-600 disabled:bg-green-600 text-white py-1 px-4 rounded"
                  >
                    {links.length < 1 ? (
                      "Enter Web Urls"
                    ) : // : !formValues.email
                    // ? "Enter Your Email"
                    loadingGetOccurence ? (
                      <Spinner />
                    ) : loading ? (
                      "Scraping Forms..."
                    ) : (
                      "Scrap Forms"
                    )}
                  </button>

                  <button
                    onClick={handleDownLoadFile}
                    disabled={links.length < 1 || loadingDownload}
                    className="bg-green-700 hover:bg-green-600 text-white py-1 px-4 rounded flex items-center"
                  >
                    <FaFileExcel />
                    <p>
                      {links.length < 1 ? (
                        "Download"
                      ) : loadingDownload ? (
                        <Spinner />
                      ) : (
                        "Download"
                      )}
                    </p>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Additional section */}
        {loadingCreate ? (
          <div className="text-center mt-5">
            <div
              className="inline-block h-8 w-8 animate-spin rounded-full text-[#005734] border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
              role="status"
            >
              <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
                Loading...
              </span>
            </div>
          </div>
        ) : (
          formData && (
            <div className="container mx-auto overflow-hidden max-w-[800px]">
              <Accordion>
                {Array.isArray(formData) ? (
                  formData.map((data, index) => (
                    <div key={index}>
                      <DynamicForm
                        formData={data}
                        webUrl={links}
                        email={email}
                      />
                    </div>
                  ))
                ) : (
                  <div>
                    <DynamicForm
                      formData={formData}
                      webUrl={links}
                      email={email}
                    />
                  </div>
                )}
              </Accordion>
            </div>
          )
        )}

        <FileUpload urls={links} />

        <div className="flex justify-center mt-3">
          <a href="https://visitorbadge.io/status?path=https%3A%2F%2Fll05-ai-dowell.github.io%2F100107-DowellEmailExtractor%2F">
            <img
              style={{ width: "100px", height: "auto" }}
              src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fll05-ai-dowell.github.io%2F100107-DowellEmailExtractor%2F&labelColor=%23005734&countColor=%23697689&style=plastic&labelStyle=upper"
            />
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;
