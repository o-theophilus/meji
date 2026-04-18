import { app } from '$lib/store.svelte.js';

const get_axis_from_area = (area) => {
	if (!area) return null;

	area = area.trim().toLowerCase();

	for (const axis in app.axis_map) {
		for (const a of app.axis_map[axis].areas) {
			if (a.toLowerCase() === area) {
				return axis;
			}
		}
	}

	return null;
}

const get_highest_price = (items, to_area, delivery_type = null) => {	
	let price = 0;
	const to_axis = get_axis_from_area(to_area, app.axis_map);

	for (const x of items) {
		const from_area = x.package?.area || 'igando';
		const from_axis = get_axis_from_area(from_area, app.axis_map);

		const route = app.price_map[from_axis][to_axis];
		const _price =
			delivery_type == 'express' ? route.express : route.price;
		if (_price > price) {
			price = _price;
		}
	}

	return price;
}

export const get_delivery_cost = (items, toArea, delivery_type = null) => {
	let totalWeight = 0;
	let totalVolume = 0;
	for (const x of items) {
		totalWeight += (x.package.weight || 0) * x.quantity;
		totalVolume +=
			(x.package.length || 0)
			* (x.package.breadth || 0)
			* (x.package.height || 0)
			* x.quantity;;

	}
	const volumetricWeight = totalVolume / 5000;
	const chargeableWeight = Math.max(totalWeight, volumetricWeight);

	let cost = get_highest_price(items, toArea, app.price_map, app.axis_map, delivery_type);
	if (chargeableWeight > 5) {
		cost += (chargeableWeight - 5) * 500;
	}
	if (totalVolume > 200000) {
		cost += 1000;
	}
	return Math.floor(cost);
}