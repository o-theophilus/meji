import { writable } from 'svelte/store';

export const showHeader = writable(true);
export const openMobileMenu = writable(false);
export const isMobile = writable(true);

export const showAvatarPanel = writable(false);
export const module = writable();


export const loading = writable(false);

export const user = writable();

export const _tick = writable("");
export const tick = (data)=> {
	_tick.set(data);
}

export const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export const months = [
	'January',
	'February',
	'March',
	'April',
	'May',
	'June',
	'July',
	'August',
	'September',
	'October',
	'November',
	'December'
];

export const ordinal_suffix_of = (i) => {
	var j = i % 10,
		k = i % 100;
	if (j == 1 && k != 11) {
		return i + 'st';
	}
	if (j == 2 && k != 12) {
		return i + 'nd';
	}
	if (j == 3 && k != 13) {
		return i + 'rd';
	}
	return i + 'th';
};


