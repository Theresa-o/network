document.addEventListener('DOMContentLoaded', function () {
    const likeIcon = document.querySelector("#like-button")
    likeIcon.addEventListener("click", handleLike)

    function handleLike(event) {
        //save the parent element in id
        let id = parseInt(event.target.parentElement.dataset.id)
        let likes = parseInt(event.target.previousElementSibling.innerText)

        fetch(`/updatelike/${id}`, {
            method: "POST",
        })
            .then(response => response.json())
            .then((data) => {

                // Saving data from response
                const likes = data.likes
                const likesPost = data.likesPost

                let likeButton = document.getElementById("like-button");

                // Adjust like variable depending on the like count
                if (likes <= 1) {
                    event.target.previousElementSibling.innerHTML = `${likes} like`
                }
                else {
                    event.target.previousElementSibling.innerHTML = `${likes} likes`
                }
            })
        // .then((data) => {
        //     document.querySelector('#likeCount').innerHTML = `${data.likes} ${data.likes <= 1 ? "like" : "likes"}`
        // })
        // event.target.previousElementSibling.innerHTML = `${likes} ${likes <= 1 ? "like" : "likes"}`;

    }
})

// function handleLike(event) {
//     event.preventDefault()
//     let form = event.target.parentElement
//     let
