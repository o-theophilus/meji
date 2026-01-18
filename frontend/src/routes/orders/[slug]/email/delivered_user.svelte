<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
	import Table from './_email.items_table.svelte';
	import User from './_email.user.svelte';
	import Date from './_email.date.svelte';

	let { order, datetime, items } = $props();
</script>

<EmailTemplate>
	Dear {'{'}name{'}'},
	<br />
	<br />
	Your order:
	<a
		style="text-decoration: none; color: #1d9bf0; text-transform: uppercase;"
		href="{page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key.substring(0, 8)}
	</a>
	has been delivered.

	<Table {items} />
	<User label="Receiver" receiver={order.receiver}></User>
	<Date datetime={order.delivery_date}></Date>

	<hr style="border-color: gray; margin: 24px 0;" />

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</EmailTemplate>
