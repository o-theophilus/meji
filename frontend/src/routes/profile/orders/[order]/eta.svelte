<script>
	import { module, days, months, ordinal_suffix_of } from '$lib/store.js';

	import Card from '$lib/card.svelte';
	import Button from '$lib/button.svelte';

	import Form from './order_eta_form.svelte';

	export let order;
	export let admin = false;

	let date, _date, time, period_of_day;
	$: {
		let date_time = order.delivery_date.split('T');
		date = date_time[0];
		_date = new Date(date);
		time = date_time[1];

		let hour = parseInt(time.split(':')[0]);

		if (hour < 12) {
			period_of_day = 'Morning';
		} else if (hour < 16) {
			period_of_day = 'Afternoon';
		} else {
			period_of_day = 'Evening';
		}
	}
</script>

<Card>
	<div class="title">
		Estimated time of delivery

		{#if order.status == 'ordered' && admin}
			<Button
				class="primary"
				icon="edit"
				on:click={() => {
					$module = {
						module: Form,
						data: {
							key: order.key,
							date,
							time
						}
					};
				}}
			/>
		{/if}
	</div>

	<p>
		To be delivered on or before
		<span>
			{days[_date.getDay()]},
			{ordinal_suffix_of(_date.getDate())} of
			{months[_date.getMonth()]}
			{_date.getFullYear()}
		</span>
		. Time:
		<span>
			{period_of_day}
		</span>.
	</p>
</Card>

<style>
	span {
		font-weight: 500;
	}
</style>
