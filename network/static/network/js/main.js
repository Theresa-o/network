document.addEventListener('DOMContentLoaded', function () {
    const likeIcon = document.querySelector("#likeBtn")
    likeIcon.addEventListener("click", handleLike)

    const likeButton = (event) => {
        id = parseInt(event.target.parentElement.dataset.id)
        let likes = document.querySelector("#likeCount")
        num = parseInt(likes.innerText)
        num += 1
        likes.innerText = num

        fetch(`/updatelike/${id}`, {
            method: "POST",
            headers: {
                "Accept": 'application/json',
                "Content-Type": 'application/json'
            }
        })
    }
})