<script>
	import { days, months, ordinal_suffix_of } from '$lib/store.js';

	export let order;

	$: if (order.delivery_date) {
		order.delivery_date = new Date(order.delivery_date);
	} else {
		let temp = new Date();
		temp.setDate(temp.getDate() + 4);
		temp.setHours(10, 0, 0, 0);
		order.delivery_date = temp;
	}
</script>

<div class="bold">
	Estimated time of delivery:
	<slot />
</div>

<p>
	To be delivered on or before
	<span class="bold">
		{days[order.delivery_date.getDay()]},
		{ordinal_suffix_of(order.delivery_date.getDate())} of
		{months[order.delivery_date.getMonth()]}
		{order.delivery_date.getFullYear()}
	</span>
	. Time:
	<span class="bold">
		{#if order.delivery_date.getHours() < 12}
			Morning
		{:else if order.delivery_date.getHours() < 16}
			Afternoon
		{:else}
			Evening
		{/if}
	</span>.
</p>

<style>
	.bold {
		font-weight: 700;
		color: var(--ac1);
	}
</style>
