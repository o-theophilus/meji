<script>
	import { module, days, months, ordinal_suffix_of } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Form from './eta__form.svelte';

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

<div class="title">
	<b> Estimated time of delivery </b>

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
	<span class="bold">
		{days[_date.getDay()]},
		{ordinal_suffix_of(_date.getDate())} of
		{months[_date.getMonth()]}
		{_date.getFullYear()}
	</span>
	. Time:
	<span class="bold">
		{period_of_day}
	</span>.
</p>

<style>
	.title {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.bold {
		font-weight: 500;
	}
</style>
