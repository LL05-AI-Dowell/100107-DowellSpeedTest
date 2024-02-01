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
          product_number: "UXLIVINGLAB005",
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
        <Modal.Header closeButton></Modal.Header>
        <Modal.Body>
          <div className="modal-divs">
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
                  <div>
                    <Button
                      variant="danger"
                      onClick={() => setOpenModal(false)}
                    >
                      Cancel
                    </Button>{" "}
                    <Button variant="success">Contribute</Button>
                  </div>
                </>
              ) : // experience is less than 4
              showOccurrence && occurrence < 4 && occurrence !== null ? (
                <>
                  <p>Your experience count is {occurrence}!</p>
                  <div>
                    <Button
                      variant="success"
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
                    <div>
                      <Button
                        variant="success"
                        onClick={() => {
                          setOpenModal(false);
                          handleFormData();
                        }}
                      >
                        Continue
                      </Button>{" "}
                      <Button variant="secondary">Contribute</Button>
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
                  variant={hasCoupon ? "danger" : "primary"}
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
                <Button
                  disabled={!coupon || loading}
                  onClick={handleRedeemCoupon}
                >
                  {loading ? <Spinner /> : "Redeem"}
                </Button>
              </div>
              <div>
                {message?.error && (
                  <Alert variant="danger">{message?.text}</Alert>
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
