const uploadBox = document.getElementById('upload-box');
const imageInput = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');
const previewImage = document.getElementById('preview-image');

// 업로드 박스를 클릭하면 파일 선택 창 열기
uploadBox.addEventListener('click', function() {
    imageInput.click();
});

// 파일 선택 시 미리보기 표시
imageInput.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        displayImagePreview(file);
    } else {
        imagePreview.style.display = 'none';
    }
});

// 드래그된 파일을 업로드 박스에 드롭했을 때 처리
uploadBox.addEventListener('dragover', function(event) {
    event.preventDefault(); // 기본 동작(파일 열기) 취소
    uploadBox.style.backgroundColor = '#f0f8ff'; // 드래그 중일 때 배경색 변경
});

uploadBox.addEventListener('dragleave', function() {
    uploadBox.style.backgroundColor = '#ffffff'; // 드래그를 벗어났을 때 원래 배경으로
});

uploadBox.addEventListener('drop', function(event) {
    event.preventDefault(); // 기본 동작(파일 열기) 취소
    uploadBox.style.backgroundColor = '#ffffff'; // 드래그 후 원래 배경으로

    const file = event.dataTransfer.files[0]; // 드롭된 파일 가져오기
    if (file) {
        displayImagePreview(file); // 미리보기 함수 호출
    }
});

// 이미지 미리보기 함수
function displayImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        previewImage.src = e.target.result;
        imagePreview.style.display = 'block';
        changeUploadBoxStyle();
    };
    reader.readAsDataURL(file);
}

// 업로드 박스 스타일 변경 함수 (이미지 업로드 후)
function changeUploadBoxStyle() {
    uploadBox.style.display = 'block';
    uploadBox.style.justifyContent = 'flex-start'; // 배경색을 연두색으로 변경
    uploadBox.style.alignItems = "stretch";
    uploadBox.querySelector('p').style.display = "None";
}