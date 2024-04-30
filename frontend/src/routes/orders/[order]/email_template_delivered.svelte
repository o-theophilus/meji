<script>
	import Template from '$lib/email_template.svelte';
	import Items from './email_template__items.svelte';
	import Receiver from './email_template__receiver.svelte';
	import Order_url from './email_template__order_url.svelte';

	export let order;
	export let items;
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
