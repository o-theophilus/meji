<script>
	import Template from '$lib/email_template.svelte';
	import Items from './email_template__items.svelte';
	import Receiver from './email_template__receiver.svelte';
	import Order_url from './email_template__order_url.svelte';

	export let order;
	export let items;
	console.log(items);

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
	Your order:
	<Order_url {order} />
	has been delivered.
	<br />
	<br />
	<Receiver {order} />
	<br />
	<br />
	<Items {items} />
	<br />
	<br />
	Thank you for your patronage.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
