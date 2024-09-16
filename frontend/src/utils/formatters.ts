import dayjs from 'dayjs';

export function formatDate(dateString: string): string {
  return dayjs(dateString).format('MMMM D, YYYY');
}

export function formatNumber(value: number): string {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength - 3) + '...';
}