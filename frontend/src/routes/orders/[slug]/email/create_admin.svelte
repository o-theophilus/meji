<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
	import Table from './_email.items_table.svelte';
	import User from './_email.user.svelte';
	import Date from './_email.date.svelte';

	let { order, items } = $props();
</script>

<EmailTemplate>
	Dear Admin,
	<br />
	<br />
	Kindly see the order
	<a
		style="text-decoration: none; color: #1d9bf0; text-transform: uppercase;"
		href="{page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key.substring(0, 8)}
	</a>
	from

	<a
		style="text-decoration: none; color: #1d9bf0;"
		href="{page.url.origin}/@{'{'}username{'}'}"
		target="_blank"
	>
		{'{'}name{'}'}
	</a>
	below.

	<Table {items} />
	<User label="Receiver" receiver={order.receiver}></User>
	<Date datetime={order.timeline.delivery_date}></Date>

	<hr style="border-color: gray; margin: 24px 0;" />

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</EmailTemplate>
