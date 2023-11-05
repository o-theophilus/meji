<script>
	import { page } from '$app/stores';

	import { days, months, ordinal_suffix_of } from '$lib/store.js';
	import Template from '$lib/email_template.svelte';

	export let order;
	let r = order.receiver;
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
	Dear {'{'}name{'}'}
	<br />
	<br />
	We are currently processing your order:
	<a
		style="
	text-decoration: none;
	color: #1d9bf0;
	"
		href="{$page.url.origin}/admin/order/{order.key}"
		target="_blank"
	>
		{order.key}
	</a>.
	<br />
	<br />
	The item{s} will be delivered to:
	<br />
	<br />
	Name:
	{r.name}
	<br />
	Phone:
	{r.phone}
	<br />
	Address:
	{a.line}, {a.local_area}, {a.state}, {a.country}, {a.postal_code}.
	<br />
	Date:
	{days[dt.getDay()]},
	{ordinal_suffix_of(dt.getDate())} of
	{months[dt.getMonth()]}
	{dt.getFullYear()}
	<br />
	Time:
	{date_time[1]}{period_of_day == 'Morning' ? 'am' : 'pm'}, {period_of_day}.
	<br />
	<br />
	<b>Item{s}:</b>
	<br />
	<br />
	{#each order.items as x}
		<img
			src="{x.photo}/40"
			alt={x.name}
			style="
		width:40px; 
height: 40px; 
object-fit: cover;
margin-right:10px;
border-radius: 8px;
"
		/>
		<div
			style="
		display:inline-block;
		"
		>
			<a
				style="
text-decoration: none;
color: #1d9bf0;
font-weight: 500;
"
				href="{$page.url.origin}/{x.slug}"
				target="_blank"
			>
				{x.name}
			</a>
			<br />
			{#each Object.entries(x.variation) as [key, value], i}
				{#if i != 0},{/if}
				{key}:

				{@const v = value.split(':')}
				{#if v[0]}
					{v[0]}
				{/if}

				{#if v[1]}
					<div
						style="
		display:inline-block;
		width:16px; 
		height: 16px; 
		border:2px solid gray;
		border-radius:50%;
		background-color:{v[1]}
		"
					/>
				{/if}
			{/each}

			{#if x.quantity > 1}
				, quantity: x{x.quantity}
			{/if}
		</div>
		<br />
		<br />
	{/each}

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
