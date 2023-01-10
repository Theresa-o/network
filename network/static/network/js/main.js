document.addEventListener('DOMContentLoaded', function () {
    const likeIcon = document.querySelector("#likeBtn")
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
                if (data.likes <= 1) {
                    document.querySelector('#likeCount').innerHTML = `${likes + 1} like`
                }
                else {
                    document.querySelector('#likeCount').innerHTML = `${likes + 1} likes`
                }

            })
    }
})