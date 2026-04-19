<script>
	import { page } from '$app/state';
	import { EmailTemplate } from '$lib/layout';
	import Table from './_email.items_table.svelte';

	let { order, items } = $props();
</script>

<EmailTemplate>
	Dear {'{'}name{'}'},
	<br />
	<br />
	You have requested to return your order:
	<a
		style="text-decoration: none; color: #1d9bf0; text-transform: uppercase;"
		href="{page.url.origin}/orders/{order.key}"
		target="_blank"
	>
		{order.key.substring(0, 8)}
	</a>. Kindly return the ordered item{items.length > 1 ? 's' : ''} within 3 days of requesting this
	return.

	<Table {items} />

	<hr style="border-color: gray; margin: 24px 0;" />

	Best regards,
	<br />
	<br />
	<b> Meji </b>
</EmailTemplate>
