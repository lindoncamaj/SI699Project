import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Recs = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state || {}; // Get form data from state

  const handleLinkClick = (make, model, year) => {
    const data = {
      "make": make,
      "model": model,
      "year": year
    }
    // Navigate to the recommendations page with the car make as a query parameter
    axios.post("http://localhost:8080/lists", data).then((response) => {navigate("/listings", {state: response.data})});
  };


  return (
    <div>
      <h1>Recommendations</h1>
      <ul>
        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item1.make, formData.item1.model, formData.item1.year);
        }}>{formData.item1.year} {formData.item1.make} {formData.item1.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item2.make, formData.item2.model, formData.item2.year);
        }}>{formData.item2.year} {formData.item2.make} {formData.item2.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item3.make, formData.item3.model, formData.item3.year);
        }}>{formData.item3.year} {formData.item3.make} {formData.item3.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item4.make, formData.item4.model, formData.item4.year);
        }}>{formData.item4.year} {formData.item4.make} {formData.item4.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item5.make, formData.item5.model, formData.item5.year);
        }}>{formData.item5.year} {formData.item5.make} {formData.item5.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item6.make, formData.item6.model, formData.item6.year);
        }}>{formData.item6.year} {formData.item6.make} {formData.item6.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item7.make, formData.item7.model, formData.item7.year);
        }}>{formData.item7.year} {formData.item7.make} {formData.item7.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item8.make, formData.item8.model, formData.item8.year);
        }}>{formData.item8.year} {formData.item8.make} {formData.item8.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item9.make, formData.item9.model, formData.item9.year);
        }}>{formData.item9.year} {formData.item9.make} {formData.item9.model}</a></li>

        <li><a href="#" onClick={(e) => {
          e.preventDefault();
          handleLinkClick(formData.item10.make, formData.item10.model, formData.item10.year);
        }}>{formData.item10.year} {formData.item10.make} {formData.item10.model}</a></li>
      </ul>
    </div>
  );
};

export default Recs;
