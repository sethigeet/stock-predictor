import { FC } from "react";

interface LoadingIndicatorProps {
  loading: boolean;
}

export const LoadingIndicator: FC<LoadingIndicatorProps> = ({ loading }) => {
  if (!loading) {
    return null;
  }

  return (
    <div className="absolute inset-0 grid place-items-center bg-black/75">
      <span className="loading loading-spinner text-primary"></span>
    </div>
  );
};
