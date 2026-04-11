<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
	import Table from './_email.items_table.svelte';

	let { order, items } = $props();
</script>

<EmailTemplate>
	Dear Admin,
	<br />
	<br />
	The order
	<a
		style="text-decoration: none; color: #1d9bf0; text-transform: uppercase;"
		href="{page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key.substring(0, 8)}
	</a>
	had been returned sucessfully by:
	<a
		style="text-decoration: none; color: #1d9bf0;"
		href="{page.url.origin}/@{'{'}username{'}'}"
		target="_blank"
	>
		{'{'}name{'}'}
	</a>. Please check the order details and take necessary actions.

	<Table {items} />

	<hr style="border-color: gray; margin: 24px 0;" />

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</EmailTemplate>
