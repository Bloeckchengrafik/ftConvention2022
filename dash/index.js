fetched_data = {
    "sorted": {
        "31007": [2,8]
    },
    "current": {
        "pid": 35077,
        "pos": [7, 7]
    }
}

box_lookup = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]

emptyimg = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="

partnr = document.querySelector("#partnr")
imges = document.querySelector("#image")
pos = document.querySelector("#pos")

async function reloadFrom(data) {
    imgdata = []

    sorted = data["sorted"]

    for (let i = 0; i<6; i++) {
        rowdata = []
        for (let x = 0; x<6; x++) {
            rowdata.push(emptyimg)
        }
        
        imgdata.push(rowdata)
    }

    for (let id in sorted) {
        image = "pictures/" + id + ".png"

        console.log("---")
        console.log("picture: ", image);

        x = sorted[id][0]-1
        y = sorted[id][1]-1

        boxid = 0

        if(x < 3) {
            boxid = 3
        } else {
            x -= 3;
        }

        if (y < 3) {
            boxid += 2
        } else if (y >= 3 && y < 6) {
            boxid +=1
            y -= 3
        } else {
            y -= 6
        }

        console.log("boxid: ", boxid);
        console.log("pos in box: [", x, ", ", y, "]")
        
        cellid = box_lookup[x][y]

        console.log("cellid: ", cellid)
        imgdata[boxid][cellid] = image
    }

    for (let bid = 0; bid<6; bid++) {
        row = imgdata[bid]
        rowchild = positions.children[bid]
        for (let cid = 0; cid<6; cid++) {
            img = row[cid]

            rowchild.children[cid].children[0].src = img
        }
    }

    partnr.innerHTML = data["current"]["pid"]
    imges.src = "pictures/" + data["current"]["pid"] + ".png"
    pos.innerHTML = data["current"]["pos"]
}

function reload() {
    fetch("/data").then(data => {
        reloadFrom(data.json())
    })
}

setInterval(reload, 1000);