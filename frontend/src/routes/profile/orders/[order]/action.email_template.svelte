<script>
	import { page } from '$app/stores';

	import { days, months, ordinal_suffix_of } from '$lib/store.js';
	import Template from '$lib/email_template.svelte';

	export let order;
	export let user;
	let r = order.recipient;
	let a = r.address;

	let s = order.items.length > 1 ? 's' : '';
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

<Template>
	Dear Admin
	<br />
	<br />
	Kindly see order Information below:
	<br />
	<br />
	<b> Order ID </b>
	<br />
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
	<br />
	<br />
	<b>Item{s}</b>
	<br />
	<br />
	{#each order.items as x}
		<a
			style="
	text-decoration: none;
	color: #1d9bf0;
	"
			href="{$page.url.origin}/{x.slug}"
			target="_blank"
		>
			<img
				src="{x.photo}/40"
				alt="item.name"
				style="
	width:40px; 
	height: 40px; 
	object-fit: cover;
	margin-right:10px
	"
			/>
			{x.name}

			{#each Object.entries(x.variation) as [key, value], i}
				, {key}: {value}
			{/each}

			{#if x.quantity > 1}
				(x{x.quantity})
			{/if}
		</a>
		<br />
		<br />
	{/each}
	<b>From User</b>
	<br />
	Name:
	<a
		style="
text-decoration: none;
color: #1d9bf0;
"
		href="{$page.url.origin}/admin/user/{user.key}"
		target="_blank"
	>
		{user.name}:
	</a>
	<br />
	Phone: {user.phone}:
	<br />
	Email: {user.email}:
	<br />
	<br />
	<b>Delivery Information</b>
	<br />
	Name: {r.name}
	<br />
	Phone: {r.phone}
	<br />
	Address: {a.line}, {a.local_area}, {a.state}, {a.country}, {a.postal_code}.
	<br />
	<br />
	The item{s} should be delivered on or before
	<b>
		{days[dt.getDay()]},
		{ordinal_suffix_of(dt.getDate())} of
		{months[dt.getMonth()]}
		{dt.getFullYear()}
	</b>. Time:
	<b>
		{date_time[1]}, {period_of_day}
	</b>.
</Template>
