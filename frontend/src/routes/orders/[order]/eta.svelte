<script>
	import { user, module, days, months, ordinal_suffix_of } from '$lib/store.js';

	import Button from '$lib/button.svelte';
	import Form from './_eta_form.svelte';

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
	Estimated time of delivery

	{#if order.status == 'ordered' && $user.roles.includes('admin')}
		<Button
			name="Edit"
			class="link"
			on:click={() => {
				$module = {
					module: Form,
					key: order.key,
					date: date_time[0],
					time: date_time[1]
				};
			}}
		/>
	{/if}
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
	p {
		color: var(--ac2);
	}
	.bold {
		font-weight: 500;
	}
</style>
