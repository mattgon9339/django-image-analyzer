import React, { useState, useEffect } from "react";
import axios from "axios";
import Swal from "sweetalert2";
import { Link } from "react-router-dom";
import InfiniteScroll from "react-infinite-scroll-component";
import { formatDate } from "../utils";
import { API_HOST } from "../env";

const Home = ({ headers }) => {
    // State variables to manage image-related data
    const [selectedImage, setSelectedImage] = useState(null);
    const [images, setImages] = useState([]);
    const [imageId, setImageId] = useState(null);
    const [description, setDescription] = useState("");
    const [comment, setComment] = useState("");
    const [lastImageId, setLastImageId] = useState(0);
    const [isEndItem, setIsEndItem] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    
    // Function to load images using infinite scroll
    const loadImages = () => {
        const customHeaders = {...headers.headers, ...{ "last-image-id": lastImageId }};
        axios.get(`${API_HOST}/api/images/`, {headers: customHeaders})
        .then(res => {
            const { images: _images } = res.data;
            if (_images.length > 0 && !isEndItem) {
                setImages(prev => [...prev, ..._images]);
                setLastImageId(_images[_images.length - 1].id);
            } else {
                setIsEndItem(true);
            }
        })
        .catch(err => {
            // Display an error message using SweetAlert2
            Swal.fire({
                title: "Image Loading Failed",
                text: err.toString(),
                icon: "error",
                confirmButtonText: "OK"
            });
        });
    };

    // Load initial images on component mount
    useEffect(() => {
        loadImages();
    }, []);

    // Load initial images on component mount
    const analyzeImage = async () => {
        let formData = new FormData();
        formData.set("file", selectedImage);
        setIsLoading(true);

        // Make a POST request to analyze the image
        const { data, status } = await axios.post(`${API_HOST}/api/analyze-image/`, formData, headers);

        // Handle the response
        if (status === 200) {
            setImageId(data.image_id);
            setDescription(data.description);

            // Display a success message using SweetAlert2
            Swal.fire({
                title: "New Image Added",
                icon: "success",
                confirmButtonText: "OK"
            });

            // If at the end of the image list, add the new image
            if (isEndItem) {
                setImages([...images, {
                    id: data.image_id,
                    description: data.description,
                    image: data.image,
                    created_at: new Date()
                }]);
            }
        }

        // Reset loading state
        setIsLoading(false);
    };

    // Render the component
    return (
        <div className="container mt-4">
            <div className="row">
                <div className="col-md-4">
                    {/* Upload Image Section */}
                    <h1>Upload Image</h1>
            
                    {!isLoading ? (
                        <>
                            {selectedImage && (
                            <div>
                                <img
                                    alt="not found"
                                    width={"250px"}
                                    src={URL.createObjectURL(selectedImage)}
                                />
                                <br />
                                <button className="btn btn-danger" onClick={() => setSelectedImage(null)}>Remove</button>
                                <button className="btn btn-primary m-1" onClick={() => analyzeImage()}>Analyze</button>
                            </div>
                            )}
                            <br />

                            <input
                                type="file"
                                name="myImage"
                                onChange={(event) => {
                                    setSelectedImage(event.target.files[0]);
                                }}
                            />
                        </>
                    ) : (
                        <h6>Analyzing...</h6>
                    )}

                    <br /><br /><br />

                    {/* Description and Comment Sections */}
                    {description ? (
                        <>
                            <h5><i>Description:</i></h5>
                            <span>{description}</span>
                            <br /><br />
                        </>
                    ) : ""}

                    {description ? (<>
                        <h5><i>Comment:</i></h5>
                        <input type="text" className="form-control" 
                            value={comment}
                            onChange={(event) => setComment(event.target.value)}
                            onKeyUp={async (event) => {
                                if (event.key === "Enter") {
                                    await axios.post(`${API_HOST}/api/image/${imageId}/comment/`, { comment }, headers);
                                    setComment("");
                                    Swal.fire({
                                        title: "Comment Added",
                                        text: comment,
                                        icon: "success",
                                        confirmButtonText: "OK"
                                    });
                                }
                            }}
                        />
                    </>) : ""}
                </div>
                <div className="col-md-8">
                    {/* Analyzed Images Section */}
                    <h1>Analyzed Images</h1>
                    <br />
                    <InfiniteScroll
                        dataLength={images?.length || 0}
                        next={loadImages}
                        hasMore={true}
                        loader={""}
                        endMessage={""}
                    >
                        {images?.map(image => {
                            return (
                                <div className="mb-4">
                                    <Link to={`/image/${image.id}`} className="text-decoration-none">
                                        <img src={API_HOST + image.image} height={200} key={image.image} />
                                    </Link>
                                    <br />
                                    <span><b>Description:</b> {image.description}</span>
                                    <br />
                                    <span style={{fontSize: "12px", color: "grey"}}>created at: {formatDate(new Date(image.created_at))}</span>
                                </div>
                            );
                        })}
                    </InfiniteScroll>
                </div>
            </div>
        </div>
    );
  };

export default Home;