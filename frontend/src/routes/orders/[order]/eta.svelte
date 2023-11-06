<script>
	import { days, months, ordinal_suffix_of } from '$lib/store.js';

	export let order;
	let date_time, dt, period_of_day;

	$: {
		date_time = order.delivery_date.split('T');
		dt = new Date(date_time[0]);

		let hour = parseInt(date_time[1].split(':')[0]);
		if (hour < 12) {
			period_of_day = 'Morning';
		} else if (hour < 16) {
			period_of_day = 'Afternoon';
		} else {
			period_of_day = 'Evening';
		}
	}
</script>

<div class="bold">
	Estimated time of delivery:

	<slot />
</div>

<p>
	To be delivered on or before
	<span class="bold">
		{days[dt.getDay()]},
		{ordinal_suffix_of(dt.getDate())} of
		{months[dt.getMonth()]}
		{dt.getFullYear()}
	</span>
	. Time:
	<span class="bold">
		{period_of_day}
	</span>.
</p>

<style>
	.bold {
		font-weight: 500;
		color: var(--ac1);
	}
</style>
