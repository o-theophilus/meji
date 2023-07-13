<script>
	import { page } from '$app/stores';

	import { days, months, ordinal_suffix_of } from '$lib/store.js';
	import Template from '$lib/comp/email_template.svelte';

	export let order;
	export let user = {};

	let s = order.items.length > 1 ? 's' : '';
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

<Template>
	Hello {user.name},
	<br />
	<br />
	You have ordered for the following item{s}:
	<br />
	<br />
	<b>Item{s}</b>
	<br />
	<br />
	{#each order.items as item}
		<a
			style="
	text-decoration: none;
	color: #1d9bf0;
	"
			href="{$page.url.origin}/{item.slug}"
			target="_blank"
		>
			<img
				src={item.photo}
				alt="item.name"
				style="width:40px; 
	height: 40px; 
	object-fit: cover;
	margin-right:10px
	"
			/>
			{item.name}

			{#if item.quantity > 1}
				(x{item.quantity})
			{/if}
		</a>
		<br />
	{/each}
	<br />
	The item{s} will be delivered on or before
	<b>
		{days[_date.getDay()]},
		{ordinal_suffix_of(_date.getDate())} of
		{months[_date.getMonth()]}
		{_date.getFullYear()}
	</b>. Time:
	<b>
		{period_of_day}
	</b>.

	<br />
	<br />
	<span
		style="
	font-size: x-small;"
	>
		You can reach out to our customer service center on: 08067397793
		<br />
		Order ID:

		<a
			style="
	text-decoration: none;
	color: #1d9bf0;
	"
			href="{$page.url.origin}/admin/order/{order.key}"
			target="_blank"
		>
			{order.key}
		</a>
	</span>
</Template>
