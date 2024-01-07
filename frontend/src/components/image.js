import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import Swal from "sweetalert2";
import { Link } from "react-router-dom";
import InfiniteScroll from "react-infinite-scroll-component";
import { formatDate } from "../utils";
import { API_HOST } from "../env";

const Image = ({ headers }) => {
    // Retrieve parameters from the URL
    const params = useParams();

    // State variables for image details, comments, etc.
    const [image, setImage] = useState(null);
    const [comments, setComments] = useState([]);
    const [lastCommentId, setLastCommentId] = useState(0);
    const [isEndItem, setIsEndItem] = useState(false);
    const [newComment, setNewComment] = useState("");

    // Function to load image details
    const loadImageDetail = () => {
        // Set custom headers, including the last comment id
        const customHeaders = {...headers.headers, ...{ "last-comment-id": lastCommentId }};

        // Fetch image details from the API
        axios.get(`${API_HOST}/api/image/${params.id}/`, {headers: customHeaders})
        .then(res => {
            const { image, comments: _comments } = res.data;

            // Update state variables based on API response
            setImage(image);
            if (_comments.length > 0 && !isEndItem) {
                setComments([...comments, ..._comments]);
                setLastCommentId(_comments[_comments.length - 1].id);
            } else {
                setIsEndItem(true);
            }
        })
        .catch(err => {
            // Handle errors with a user-friendly alert
            Swal.fire({
                title: "Image Detail Loading Failed",
                text: err.toString(),
                icon: "error",
                confirmButtonText: "OK"
            });
        });
    }

    // Load image details on component mount
    useEffect(() => {
        loadImageDetail();
    }, []);

    return (
        <div className="container mt-4">
            <div className="row">
                {/* Link to navigate back to the home page */}
                <div className="mb-4"><Link to="/" className="btn btn-success">Go To Home</Link></div>

                {/* Display the main image with its description */}
                <div><img src={API_HOST + image?.image} height={300} key={image?.image} /></div>
                <h5><b><i>Description:</i></b> {image?.description}</h5>
                <br /><br />

                {/* Input field to add new comments */}
                <div>
                    <h5><i>Add Comment:</i></h5>
                    <input type="text" className="form-control mb-4"
                        value={newComment}
                        onChange={(event) => setNewComment(event.target.value)}
                        onKeyUp={async (event) => {
                            if (event.key === "Enter") {
                                await axios.post(`${API_HOST}/api/image/${params.id}/comment/`, { comment: newComment }, headers);
                                if (isEndItem) {
                                    setComments([...comments, {text: newComment, created_at: formatDate(new Date())}]);
                                }
                                setNewComment("");
                                Swal.fire({
                                    title: "Comment Added",
                                    text: newComment,
                                    icon: "success",
                                    confirmButtonText: "OK"
                                });
                            }
                        }}
                    />
                </div>

                {/* Display existing comments with infinite scrolling */}
                <h3 className="mb-3">Comments</h3>
                <div>
                    <InfiniteScroll
                        dataLength={comments.length}
                        next={loadImageDetail}
                        hasMore={true}
                        loader={""}
                        endMessage={""}
                    >
                        {comments.map(comment => {
                            // Display each comment with its creation timestamp
                            return (
                                <p key={comment.id}>
                                    {comment.text}
                                    <br />
                                    <span style={{fontSize: "12px", color: "grey"}}>created at: {formatDate(new Date(comment.created_at))}</span>
                                </p>
                            );
                        })}
                    </InfiniteScroll>
                </div>
            </div>
        </div>
    );
};

export default Image;