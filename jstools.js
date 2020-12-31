function supersearch(objectlist, properties, keyword) {
    let newobjlst = []
    for (obj of objectlist) {
        for (pro of properties) {
            if ((obj[pro]).includes(keyword)) {
                newobjlst.push(obj);
                break;
            }
        }
    }
    return newobjlst;
}

function supersort(objectlist, property, ascending = true, number = false) {
    let i, j;
    for (i = 0; i < objectlist.length; i++) {
        for (j = i; j < objectlist.length; j++) {
            if (number) {
                if (Number(objectlist[i][property]) > Number(objectlist[j][property])) {
                    let temp = objectlist[j];
                    objectlist[j] = objectlist[i];
                    objectlist[i] = temp;
                }
            } else {
                if (objectlist[i][property].toUpperCase() > objectlist[j][property].toUpperCase()) {
                    let temp = objectlist[j];
                    objectlist[j] = objectlist[i];
                    objectlist[i] = temp;
                }
            }
        }
    }
    if (!ascending) {
        return objectlist.reverse();
    } else {
        return objectlist;
    }
}