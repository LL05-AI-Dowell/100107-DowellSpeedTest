/* eslint-disable react/prop-types */
import { useEffect, useState } from "react";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Alert from "react-bootstrap/Alert";

import axios from "axios";
import Spinner from "./spinnertwo";

function OccurenceModal({
  showModal,
  setOpenModal,
  handleFormData,
  showOccurrence,
  occurrence,
  email,
}) {
  const [hasCoupon, setHasCoupon] = useState(false);
  const [coupon, setCoupon] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({
    error: false,
    text: "",
  });

  const handleCoupon = () => {
    setHasCoupon(!hasCoupon);
  };

  const handleRedeemCoupon = async () => {
    setLoading(true);
    try {
      // setLoading(true);
      const response = await axios.post(
        `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=redeem_coupon`,
        {
          email: email,
          coupon: coupon,
          product_number: "UXLIVINGLAB007",
        }
      );
      // Set the emailSent state to true when the email is sent
      setLoading(false);
      console.log(response);
    } catch (error) {
      setLoading(false);
      setMessage({
        error: true,
        text: error?.message,
      });
      console.log(message);
    }
  };

  useEffect(() => {
    setMessage(message);
  }, [message]);

  return (
    <>
      <Modal centered show={showModal} onHide={() => setOpenModal(false)}>
        <Modal.Header>
          <button
            type="button"
            className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 focus:outline-none"
            onClick={() => setOpenModal(false)}
          >
            <span className="sr-only">Close</span>
            <svg
              className="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </Modal.Header>
        <Modal.Body>
          <div className="modal-divs h-[50%]">
            <img
              style={{ width: "100px" }}
              src="https://www.uxlivinglab.org/wp-content/uploads/2023/10/image_1-3.png"
              alt="Dowell Logo"
            />

            <div style={{ fontWeight: "bold", fontSize: "20px" }}>
              Dowell Crawler
            </div>
          </div>

          <div className="modal-divs">
            {
              // experience is greater or equal to 6
              showOccurrence && occurrence >= 6 && occurrence !== null ? (
                <>
                  <p>Your experience count is {occurrence}!</p>
                  <div className="flex gap-2 justify-center">
                    <Button
                      className="bg-red-500  mt-2 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
                      onClick={() => setOpenModal(false)}
                    >
                      Cancel
                    </Button>{" "}
                    <Button className="bg-[#005734] hover:bg-green-700  mt-2 text-white font-bold py-2 px-4 rounded">
                      Contribute
                    </Button>
                  </div>
                </>
              ) : // experience is less than 4
              showOccurrence && occurrence < 4 && occurrence !== null ? (
                <>
                  <p>Your experience count is {occurrence}!</p>
                  <div>
                    <Button
                      className="bg-[#005734] mt-2 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                      onClick={() => {
                        setOpenModal(false);
                        handleFormData();
                      }}
                    >
                      Continue
                    </Button>
                  </div>
                </>
              ) : (
                // experience is greater or equal to 4 and is less than 6
                showOccurrence &&
                occurrence >= 4 &&
                occurrence < 6 &&
                occurrence !== null && (
                  <div>
                    <p>Your experience count is {occurrence}!</p>
                    <div className="flex gap-2 justify-center">
                      <Button
                        className="bg-[#005734] hover:bg-green-700  mt-2 text-white font-bold py-2 px-4 rounded"
                        onClick={() => {
                          setOpenModal(false);
                          handleFormData();
                        }}
                      >
                        Continue
                      </Button>{" "}
                      <Button className="bg-gray-500  mt-2 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded">
                        Contribute
                      </Button>
                    </div>
                  </div>
                )
              )
            }
          </div>

          {occurrence >= 4 && (
            <div className="modal-divs" style={{ marginTop: "25px" }}>
              <p>
                Do you have a coupon?{" "}
                <Button
                  className={`${
                    hasCoupon
                      ? "bg-red-500 hover:bg-red-600"
                      : "bg-[#005734] hover:bg-green-700"
                  } text-white font-bold py-2 px-4 rounded`}
                  onClick={handleCoupon}
                >
                  {hasCoupon ? "No" : "Yes"}
                </Button>
              </p>
            </div>
          )}

          {hasCoupon && (
            <div>
              <div style={{ display: "flex", gap: "5px" }}>
                <input
                  type="text"
                  className="form-control"
                  value={coupon}
                  onChange={(e) => setCoupon(e.target.value)}
                  placeholder="Enter Coupon"
                />{" "}
                <button
                  disabled={!coupon || loading}
                  className={`${
                    !coupon || loading
                      ? "bg-gray-400 cursor-not-allowed"
                      : "bg-[#005734] hover:bg-green-700"
                  } text-white font-bold py-2 px-4 rounded`}
                  onClick={handleRedeemCoupon}
                >
                  {loading ? <Spinner /> : "Redeem"}
                </button>
              </div>
              <div>
                {message?.error && (
                  <Alert className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded">
                    {message?.text}
                  </Alert>
                )}
              </div>
            </div>
          )}
        </Modal.Body>
      </Modal>
    </>
  );
}

export default OccurenceModal;
