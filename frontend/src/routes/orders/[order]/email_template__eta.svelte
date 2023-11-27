<script>
	import { days, months, ordinal_suffix_of } from '$lib/store.js';

	export let order;

	let dt, period_of_day, date_time;
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

Date:
{days[dt.getDay()]},
{ordinal_suffix_of(dt.getDate())} of
{months[dt.getMonth()]}
{dt.getFullYear()}
<br />
Time:
{date_time[1]}{period_of_day == 'Morning' ? 'am' : 'pm'}, {period_of_day}.
