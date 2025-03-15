import { useLocation } from "react-router-dom";

const Listings = () => {
    const location = useLocation();
    const listingsData = location.state || {};

    return (
        <div>
            <h1>Listings</h1>
            <ul>
                <li><a href={listingsData[0].vdp_url}>{listingsData[0].heading}</a></li>
                <li><a href={listingsData[1].vdp_url}>{listingsData[1].heading}</a></li>
                <li><a href={listingsData[2].vdp_url}>{listingsData[2].heading}</a></li>
                <li><a href={listingsData[3].vdp_url}>{listingsData[3].heading}</a></li>
                <li><a href={listingsData[4].vdp_url}>{listingsData[4].heading}</a></li>
                <li><a href={listingsData[5].vdp_url}>{listingsData[5].heading}</a></li>
                <li><a href={listingsData[6].vdp_url}>{listingsData[6].heading}</a></li>
                <li><a href={listingsData[7].vdp_url}>{listingsData[7].heading}</a></li>
                <li><a href={listingsData[8].vdp_url}>{listingsData[8].heading}</a></li>
                <li><a href={listingsData[9].vdp_url}>{listingsData[9].heading}</a></li>
            </ul>
        </div>
    );
};


export default Listings;