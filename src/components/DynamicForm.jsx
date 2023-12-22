/* eslint-disable react/prop-types */
import { useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";

const DynamicForm = ({ formData, webUrl,email }) => {
  const [formValues, setFormValues] = useState({});
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Set the form value directly
    const updatedFormValues = {
      ...formValues,
      [name]: value,
    };

    setFormValues(updatedFormValues);
  };


// function to send extracted data to email
const handleSendEmail = async (htmlContent) => {
  try {
    // setLoading(true);
    const response = await axios.post(
      `https://100085.pythonanywhere.com/api/email/`,
      {
        toname: "Dowell UX Living Lab",
        toemail: !email ? "dowell@dowellresearch.uk" : email,
        subject: `${
          email
        } result from DoWell "Contact Us Page" Extractor on ${new Date()}`,
        email_content: htmlContent
      }
    );
    // Set the emailSent state to true when the email is sent
    
    console.log(response);
  } catch (error) {
    toast.error(error ? error?.response?.data?.error : error?.message);
     console.log(error)
  }
};
 




  const handleSubmit = (e) => {
    e.preventDefault();

    // Prepare the data to send
    const dataToSend = {
      page_links: webUrl,
      form_data: [formValues],
    };

    // Send the data to the API using Axios
    setLoading(true);
    axios
      .post("https://www.uxlive.me/api/submit-contact-form/", dataToSend)
      .then((response) => {
        setLoading(false);
        toast.success(JSON.stringify(response?.data?.success));
        
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
                <p style="font-size: 1.1em">Links</p> ${" "}
                  <ul>
                    ${webUrl?.map((link) => (
                        `<li key=${link}>
                          <a href=${link}>${link}</a>
                        </li>`
                    ))}
                  </ul>
                <p style="font-size: 1.1em">Sent Form Data</p> ${" "}
                <ul>
                  ${Object.entries(formValues)
                    .map(
                      ([name, value]) =>
                        `<li key=${name}>${name} : ${value}</li>`
                    )
                    .join("")}
                </ul>
              </div>
            </div>
          </body>
        </html>
      `;

      handleSendEmail(htmlContent);
      
      
      })
      .catch((error) => {
        setLoading(false);
        toast.error(error ? error?.response?.data?.error : error?.message);
        console.error("Form data submission failed:", error);
      });
  };

  return (
    <section className="container">
      <div className="container mx-auto">
            <form onSubmit={handleSubmit} className="space-y-8">
              {formData &&
                Object?.keys(formData)?.map((fieldName, index) =>
                  fieldName !== "submit" ? (
                    <div key={index}>
                      <label
                        htmlFor={fieldName}
                        className="block mb-1 font-medium text-dark-600"
                      >
                        {fieldName}
                      </label>
                        

                      {formData[fieldName] === "textarea" ? (
                        <textarea
                          id="message"
                          rows="3"
                          onChange={handleInputChange}
                          name={fieldName}
                          value={formValues[fieldName] || ""}
                          className="block p-3 w-full text-sm text-gray-900 bg-gray-50 rounded-lg shadow-sm border border-gray-300 focus:outline-[#005734]"
                          placeholder="Leave Your Message Here."
                        ></textarea>
                      ) : (
                        <input
                          type={formData[fieldName]}
                          id="text"
                          name={fieldName}
                          value={formValues[fieldName] || ""}
                          onChange={handleInputChange}
                          className="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:outline-[#005734] w-full p-2.5"
                          placeholder={`Enter ${fieldName}`}
                          required
                        />
                      )}
                    </div>
                  ) : null
                )}

              <button
                type="submit"
                className="bg-green-700 hover:bg-green-600 text-white font-bold py-2 px-4 rounded flex items-center"
                disabled={loading}
              >
                {loading ? "Submitting Form..." : "Submit"}
              </button>
            </form>
      </div>
    </section>
  );
};

export default DynamicForm;
