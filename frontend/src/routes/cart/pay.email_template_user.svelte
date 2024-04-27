<script>
	import { page } from '$app/stores';
	import { user } from '$lib/store.js';

	import Template from '$lib/email_template.svelte';
	import Items from '../orders/[order]/email_template__items.svelte';
	import Receiver from '../orders/[order]/email_template__receiver.svelte';
	import Order_url from '../orders/[order]/email_template__order_url.svelte';
	import Datetime from '$lib/datetime.svelte';

	export let order;
	export let items;
</script>

<Template>
	Dear {$user.name}
	<br />
	<br />
	We are currently processing your order:
	<Order_url {order} />
	<br />
	<br />
	<Receiver {order} />
	<br />
	Date:
	<Datetime datetime={order.delivery_date} type="day" />,
	<Datetime datetime={order.delivery_date} type="date" style="a" />. Time:
	<Datetime datetime={order.delivery_date} type="time" />.
	<br />
	<br />
	<Items {items} />
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
