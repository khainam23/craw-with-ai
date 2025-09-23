// Nhập thư viện Mapple.js
const MappleUtil = require('C:\\Users\\khain\\Downloads\\Mapple.js');

// Thực hiện chuyển đổi
var result = MappleUtil.getWGS84FromTokyoDatum(502813.183, 128669.157);
console.log("Latitude: " + result.y + ", Longitude: " + result.x);
