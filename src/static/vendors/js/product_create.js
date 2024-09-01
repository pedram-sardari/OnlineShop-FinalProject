let count = 2
let imageInput = document.getElementById('id_image1')
let addImageBtn = document.getElementById('add-image')
addImageBtn.addEventListener('click', () => {
    let clonedImageInput = imageInput.cloneNode(true)
    clonedImageInput.name = `image${count}`
    clonedImageInput.id = `id_image${count}`
    clonedImageInput.value = ''
    imageInput.parentElement.append(clonedImageInput)
    count++
})