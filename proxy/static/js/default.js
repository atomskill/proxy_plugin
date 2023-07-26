let upload_count = 0;

window.onload = function () {
    new Table({
        element: document.getElementById("file_list"),
        headers: {
            name: {format: (x) => `<a href="/download/${x}">${x}`},
            size: {},
            modify_time: {format: (x) => (new Date(x * 1000)).toLocaleString()},
            content_type: {}
        },
        data: files,
        className: "table table-sm table-striped table-hover",
        theadClassName: "thead-dark table-sm"
    }).view();
};


/**
 * Выбор файлов для загрузки.
 */
function selectFiles() {
    let fileElem = document.getElementById("fileElem");
    if (fileElem) {
        fileElem.click();
    }
}


/**
 * Подготовка файлов для загрузки на сервер.
 *
 * @param {FileList} files - список файлов.
 */
function upload(files) {
    upload_count = files.length;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        uploadObject(file);
    }
}


/**
 * Низкоуровневая загрузка файла.
 *
 * @param {File} file - словарь, описывающий загружаемый объект
 */
function uploadObject(file) {
    let stream = new XMLHttpRequest();

    // Запрещаем перезагрузку страницы.
    window.onbeforeunload = function () {
        return "";
    };

    // Проверяем права доступа к файлу.
    const fd = new FileReader();
    fd.addEventListener("error", function () {
        uploadEnd();
    });
    fd.addEventListener("load", uploadStart);
    uploadStart();

    /**
     * Начало загрузки файла.
     */
    function uploadStart() {
        // Получаем метаинформацию объекта.
        stream.open("PUT", "/upload", true);
        stream.addEventListener("loadend", uploadEnd);

        stream.setRequestHeader("X-Name", file.name)
        stream.setRequestHeader("Content-Type", file.type)

        stream.send(file);
    }

    /**
     * Окончание загрузки файла.
     */
    function uploadEnd() {
        upload_count--;

        if (!upload_count) {
            window.onbeforeunload = undefined;
            location.reload();
        }
    }
}
